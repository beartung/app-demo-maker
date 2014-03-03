//
//  DBPageViewController.h
//  maker
//
//  Created by Bear on 2/22/14.
//  Copyright (c) 2014 Bear. All rights reserved.
//

#import <UIKit/UIKit.h>
#import "DBPage.h"
#import "DBEnv.h"
#import "DBPageView.h"
#import "DBTouchControl.h"

@interface DBPageViewController : UIViewController<UITableViewDelegate, UITableViewDataSource>

@property (nonatomic, strong) NSString * pid;
@property (nonatomic, strong) NSString * refer;
@property (nonatomic, strong) DBEnv * env;
@property (nonatomic, strong) DBPage * page;
@property (nonatomic, strong) id<DBTouchControl> handler;

-(id)initWithEnv:(DBEnv *)env pageId:(NSString *)pid referPageId:(NSString *)refer touchHandler:(id<DBTouchControl>)delegate;

@end
