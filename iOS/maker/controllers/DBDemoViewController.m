//
//  DBDemoViewController.m
//  maker
//
//  Created by Bear on 2/23/14.
//  Copyright (c) 2014 Bear. All rights reserved.
//

#import "DBDemoViewController.h"
#import "DBEnv.h"
#import "DBActionView.h"
#import "DBAction.h"
#import "DBPageViewController.h"

#import <AFNetworking.h>

@interface DBDemoViewController ()

@property (nonatomic, strong) DBEnv * env;
@property (nonatomic, strong) NSMutableDictionary * pages;
- (DBPageViewController *)getPageController:(NSString *)pid withRefer:(NSString *)refer;

@end

@implementation DBDemoViewController

- (id)initWithUrl:(NSString *)url
{
    self = [super init];
    if (self){
        self.api = url;
        self.pages = [[NSMutableDictionary alloc] init];
        self.spinner = [[UIActivityIndicatorView alloc]
                        initWithActivityIndicatorStyle:UIActivityIndicatorViewStyleGray];
        self.spinner.hidesWhenStopped = YES;
        self.spinner.center = self.view.center;
        [self.view addSubview:self.spinner];

        UITapGestureRecognizer * tt = [[UITapGestureRecognizer alloc] initWithTarget:self
                                                                              action:@selector(twoFingersTwoTaps)];
        [tt setNumberOfTapsRequired:2];
        [tt setNumberOfTouchesRequired:2];
        [[self view] addGestureRecognizer:tt];
        
        self.modalPresentationStyle = UIModalPresentationCurrentContext;
    }
    return self;
}

- (DBPageViewController *)getPageController:(NSString *)pid withRefer:(NSString *)refer
{
    DBPageViewController * pc = [self.pages valueForKey:pid];
    NSLog(@"getPageController %@, %@", pid, pc);
    if (pc == nil){
        NSLog(@"makePageController new %@", pid);
        pc = [[DBPageViewController alloc]
                    initWithEnv:self.env
                         pageId:pid
                    referPageId:refer
                   touchHandler:self];
        NSLog(@"setPage %@", pid);
        [self.pages setValue:pc forKey:pid];
    }
    return pc;
}

- (void)loadDemo:(NSString *)url
{
    [self.spinner startAnimating];
    AFHTTPRequestOperationManager *manager = [AFHTTPRequestOperationManager manager];
    [manager GET:url parameters:nil success:^(AFHTTPRequestOperation *operation, id json) {
        [self.spinner stopAnimating];
        NSLog(@"JSON: %@ %@", json, [json class]);
        self.env = [[DBEnv alloc] initWithDict:json];
        DBPageViewController * pc = [self getPageController:self.env.pageIds[0] withRefer:nil];
        [self addChildViewController:pc];
        [self.view addSubview:pc.view];
        [pc didMoveToParentViewController:self];
    } failure:^(AFHTTPRequestOperation *operation, NSError *error) {
        [self.spinner stopAnimating];
        NSLog(@"Error: %@", error);
    }];
}

- (void)viewDidLoad
{
    [super viewDidLoad];
	// Do any additional setup after loading the view.
    [self loadDemo:self.api];
    

}

- (void)didReceiveMemoryWarning
{
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

-(void)onTap:(UITapGestureRecognizer *)tap
{
    NSLog(@"onTap!!");
    DBActionView * v = (DBActionView*)tap.view;
    DBAction * a = v.action;
    NSString * pid = v.pid;
    NSString * from = a.fromPageId;
    NSString * to = a.toPageId;
    
    NSLog(@"action pid=%@, type=%@, from=%@, to=%@", pid, a.type, from, to);
    DBPage * fp = [self.env getPage:from];
    DBPage * tp = [self.env getPage:to];
    
    if ([fp.type isEqualToString:PAGE_TYPE_ITEM]){
        NSLog(@"item=%@, list=%@", fp.id, fp.parent);
        DBPage * pp = [self.env getPage:fp.parent];
        NSLog(@"list=%@, page=%@", pp.id, pp.parent);
        from = pp.parent;
        NSLog(@"action pid=%@, type=%@, from=%@, to=%@", pid, a.type, from, to);
    }
    
    if([a.type isEqualToString:ACTION_TYPE_BACK]){
        to = v.refer;
        NSLog(@"back to=%@", to);
        DBPage * bp = [self.env getPage:to];
        if ([bp.type isEqualToString:PAGE_TYPE_DIALOG]){
            to = bp.parent;
        }
    }
    
    DBPageViewController * tpc = [self getPageController:to withRefer:from];
    DBPageViewController * fpc = [self.pages valueForKey:from];

    if ([tp.type isEqualToString:PAGE_TYPE_DIALOG]){
        [self presentViewController:tpc animated:YES completion:nil];
        return;
    }else if([fp.type isEqualToString:PAGE_TYPE_DIALOG]){
        [fpc dismissViewControllerAnimated:YES completion:nil];
        if(![a.type isEqualToString:ACTION_TYPE_BACK]){
            [fpc dismissViewControllerAnimated:YES completion:nil];
            from = v.refer;
            [self animateFromPage:from toPage:to animType:a.type];
        }
    }else{
        [self animateFromPage:from toPage:to animType:a.type];
    }
    
}

-(void)animateFromPage:(NSString *)fid toPage:(NSString *)tid animType:(NSString *)atype
{
    NSLog(@"animate from %@ to %@", fid, tid);
    DBPageViewController * fpc = [self.pages valueForKey:fid];
    DBPageViewController * tpc = [self getPageController:tid withRefer:fid];
    [self addChildViewController:tpc];
    [self.view addSubview:tpc.view];
    
    CGFloat width = self.view.frame.size.width;
    CGFloat height = self.view.frame.size.height;
    if ([atype isEqualToString:ACTION_TYPE_TOUCH] || [atype isEqualToString:ACTION_TYPE_SLIDE_LEFT]){
        tpc.view.frame = CGRectMake(width, 0, width, height);
    }else if ([atype isEqualToString:ACTION_TYPE_BACK] ||[atype isEqualToString:ACTION_TYPE_SLIDE_RIGHT]){
        tpc.view.frame = CGRectMake(-width, 0, width, height);
    }else if ([atype isEqualToString:ACTION_TYPE_SLIDE_UP]){
        tpc.view.frame = CGRectMake(0, height, width, height);
    }else if ([atype isEqualToString:ACTION_TYPE_SLIDE_DOWN]){
        tpc.view.frame = CGRectMake(0, -height, width, height);
    }
    __weak id weakSelf = self;
    [self transitionFromViewController:fpc
                      toViewController:tpc
                              duration:0.4
                               options:UIViewAnimationOptionTransitionNone
                            animations:^{
                                if ([atype isEqualToString:ACTION_TYPE_TOUCH]
                                        || [atype isEqualToString:ACTION_TYPE_SLIDE_LEFT]){
                                    fpc.view.frame = CGRectMake(-width, 0, width, height);
                                }else if ([atype isEqualToString:ACTION_TYPE_BACK]
                                        ||[atype isEqualToString:ACTION_TYPE_SLIDE_RIGHT]){
                                    fpc.view.frame = CGRectMake(width, 0, width, height);
                                }else if ([atype isEqualToString:ACTION_TYPE_SLIDE_UP]){
                                    fpc.view.frame = CGRectMake(0, -height, width, height);
                                }else if ([atype isEqualToString:ACTION_TYPE_SLIDE_DOWN]){
                                    fpc.view.frame = CGRectMake(0, height, width, height);
                                }
                                tpc.view.frame = CGRectMake(0, 0, width, height);
                            }
                            completion:^(BOOL finished){
                                [tpc didMoveToParentViewController:weakSelf];
                            }];

}

-(void)print
{
    DBPageViewController * c = nil;
    for (int i = 0; i < self.childViewControllers.count; i++){
        c = self.childViewControllers[i];
        NSLog(@"child %d=%@", i, c.pid);
    }
    
    NSLog(@"view count %d", self.view.subviews.count);
    for (int i = 0; i < self.view.subviews.count; i++){
        NSLog(@"view %d=%@", i, self.view.subviews[i]);
    }
}

-(void)onSlide:(UITapGestureRecognizer *)tap
{
    
    UISwipeGestureRecognizer * sg = (UISwipeGestureRecognizer *)tap;
    
    DBActionView * v = (DBActionView*)tap.view;
    DBAction * a = v.action;
    NSString * pid = v.pid;
    NSLog(@"action pid=%@, type=%@, from=%@, to=%@", pid, a.type, a.fromPageId, a.toPageId);

    NSLog(@"onSlide!!");
    switch (sg.direction) {
        case UISwipeGestureRecognizerDirectionLeft:
            NSLog(@"UISwipeGestureRecognizerDirectionLeft");
            break;
        case UISwipeGestureRecognizerDirectionRight:
            NSLog(@"UISwipeGestureRecognizerDirectionRight");
            break;
        case UISwipeGestureRecognizerDirectionUp:
            NSLog(@"UISwipeGestureRecognizerDirectionUp");
            break;
        case UISwipeGestureRecognizerDirectionDown:
            NSLog(@"UISwipeGestureRecognizerDirectionDown");
            break;
    }
    
    [self animateFromPage:a.fromPageId toPage:a.toPageId animType:a.type];
    
}

- (void)twoFingersTwoTaps
{
    NSLog(@"Action: Two fingers, two taps");
    [self.navigationController popToRootViewControllerAnimated:YES];
}


@end
