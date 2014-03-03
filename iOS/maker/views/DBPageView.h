//
//  DBPageView.h
//  maker
//
//  Created by Bear on 2/22/14.
//  Copyright (c) 2014 Bear. All rights reserved.
//

#import <UIKit/UIKit.h>
#import "DBPage.h"
#import "DBAction.h"
#import "DBTouchControl.h"

@interface DBPageView : UIView

@property (nonatomic, strong) UIView * box;

- (id)initWithFrame:(CGRect)frame andPage:(DBPage *)page referId:(NSString *)refer touchHandler:(id<DBTouchControl>)delegate;

@end
